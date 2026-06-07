/**
 * Unheard API gateway — skeleton. (Phase 1, epics E2/E3)
 *
 * This wires the route registry into Fastify with an onSend privacy guard.
 * Handlers are stubs returning 501 until their epic lands; the point of this
 * file today is to make the privacy boundary structural, not bolted on later.
 */
import Fastify from 'fastify';
import { ROUTES } from './routes.js';
import { assertNoForbiddenFields } from './lib/serialize.js';

export function buildServer() {
  const app = Fastify({ logger: true });

  // Belt-and-suspenders: no response may contain a server-only field. (NFR-PRIV-04)
  app.addHook('onSend', async (_req, _reply, payload) => {
    if (typeof payload === 'string' && payload.startsWith('{')) {
      try {
        assertNoForbiddenFields(JSON.parse(payload));
      } catch (err) {
        // Fail closed: never ship a payload that leaks identity.
        throw err;
      }
    }
    return payload;
  });

  app.get('/healthz', async () => ({ status: 'ok' }));

  for (const r of ROUTES) {
    if (r.path === '/healthz') continue;
    const fastifyPath = r.path.replace(/:(\w+)/g, ':$1');
    app.route({
      method: r.method,
      url: fastifyPath,
      handler: async (_req, reply) => {
        reply.code(501);
        return { error: 'not_implemented', requirement: r.req, summary: r.summary };
      },
    });
  }

  return app;
}

// Run directly: `npm run dev`
if (import.meta.url === `file://${process.argv[1]}`) {
  const app = buildServer();
  const port = Number(process.env.PORT ?? 8080);
  app.listen({ port, host: '0.0.0.0' }).catch((err) => {
    app.log.error(err);
    process.exit(1);
  });
}
