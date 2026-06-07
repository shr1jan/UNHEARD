/**
 * Log scrubbing. (NFR-PRIV-03)
 *
 * Raw audio, transcripts, and (later) phone numbers must NEVER reach logs.
 * Request bodies are scrubbed before any logging. This is intentionally
 * aggressive: it redacts known-sensitive keys and any binary/audio payloads.
 */

const SENSITIVE_KEYS = new Set([
  'audio',
  'rawAudio',
  'raw_audio',
  'transcript',
  'voiceprint',
  'phone',
  'phoneNumber',
  'phone_number',
  'authorization',
  'cookie',
]);

export function scrub(value: unknown): unknown {
  if (Buffer.isBuffer?.(value) || value instanceof Uint8Array) {
    return `[redacted ${(value as Uint8Array).byteLength} bytes]`;
  }
  if (Array.isArray(value)) return value.map(scrub);
  if (value !== null && typeof value === 'object') {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      out[k] = SENSITIVE_KEYS.has(k.toLowerCase()) ? '[redacted]' : scrub(v);
    }
    return out;
  }
  return value;
}
