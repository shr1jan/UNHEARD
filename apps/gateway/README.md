# @unheard/gateway

Node.js + TypeScript API gateway (Fastify). Handles auth, feed, posts, reactions,
comments, reports, topic-follow; enqueues masking + moderation jobs; serves
signed audio URLs. (Architecture §7, epics **E2**/**E3**.)

## Status

Skeleton. Routes are declared in [`src/routes.ts`](src/routes.ts) and return `501`
until their epic lands. What is **already real and enforced**:

- **Public serializer** ([`src/lib/serialize.ts`](src/lib/serialize.ts)) — the only
  sanctioned record→wire boundary; strips server-only fields. (`NFR-PRIV-04`)
- **onSend privacy guard** ([`src/server.ts`](src/server.ts)) — fails closed if any
  response would leak an internal id.
- **Route registry guard** ([`src/routes.ts`](src/routes.ts)) — no `/users/:id`,
  `/profiles`, history/timeline surfaces can exist. (`NFR-PRIV-05`)
- **Log scrubbing** ([`src/lib/logScrub.ts`](src/lib/logScrub.ts)) — audio,
  transcripts, phone numbers never reach logs. (`NFR-PRIV-03`)

These are covered by `test/` and run in CI as the privacy gates (epic **E5**).

## Develop

```bash
npm install            # from repo root (workspaces)
npm run dev -w @unheard/gateway     # start on :8080
npm run test -w @unheard/gateway    # privacy-gate tests
npm run typecheck -w @unheard/gateway
```

## Next issues

`E2-1` anonymous auth · `E2-2` hidden internal id · `E3-2` post creation API ·
`E3-3` feed with three sorts · `E3-6` instant hard delete.
