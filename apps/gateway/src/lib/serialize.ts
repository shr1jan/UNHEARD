/**
 * Public serialization boundary. (NFR-PRIV-04, FR-ACCT-02)
 *
 * The ONLY sanctioned way to turn an internal record into a wire payload.
 * It strips a denylist of server-only fields and is verified by
 * test/serialize.test.ts. If you find yourself wanting to bypass this, that is
 * the bug.
 */

/** Fields that must never cross the wire, regardless of nesting. */
export const FORBIDDEN_FIELDS: ReadonlySet<string> = new Set([
  'internalId',
  'internal_id',
  'ownerId',
  'owner_id',
  'accountId',
  'account_id',
  'rateState',
  'rate_state',
  'banState',
  'ban_state',
  'reporterId',
  'reporter_id',
  'phoneNumber',
  'phone_number',
]);

/**
 * Recursively removes forbidden fields from an object/array tree, returning a
 * structurally-cloned, safe-to-serialize value.
 */
export function toPublic<T>(value: T): T {
  if (Array.isArray(value)) {
    return value.map((v) => toPublic(v)) as unknown as T;
  }
  if (value !== null && typeof value === 'object') {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      if (FORBIDDEN_FIELDS.has(k)) continue;
      out[k] = toPublic(v);
    }
    return out as T;
  }
  return value;
}

/** Throws if any forbidden field is present anywhere in the tree. Used as a
 *  belt-and-suspenders assertion in tests and (optionally) as an onSend hook. */
export function assertNoForbiddenFields(value: unknown, path = '$'): void {
  if (Array.isArray(value)) {
    value.forEach((v, i) => assertNoForbiddenFields(v, `${path}[${i}]`));
    return;
  }
  if (value !== null && typeof value === 'object') {
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      if (FORBIDDEN_FIELDS.has(k)) {
        throw new Error(`forbidden field "${k}" present at ${path}.${k} (NFR-PRIV-04)`);
      }
      assertNoForbiddenFields(v, `${path}.${k}`);
    }
  }
}
