# AI Call Bot Monorepo Foundation

Production-oriented foundation for a multi-tenant white-label AI voice agent platform.

## Monorepo structure

- `apps/api` — FastAPI orchestration backend
- `apps/web` — Next.js admin dashboard (scaffold placeholder for next phase)
- `docs` — architecture and planning artifacts
- `docker-compose.yml` — local development stack (Postgres, Redis, API)

## Quick start

```bash
docker compose up --build
```

API base URL: `http://localhost:8000/api/v1`
Health endpoint: `http://localhost:8000/health`

## Delivered in this commit

- Phase 1 planning artifacts in `docs/phase-1-foundation.md`.
- Phase 2 backend foundation:
  - auth
  - tenant/client/agent CRUD base
  - wizard draft persistence
  - Twilio inbound webhook resolver base
  - call session persistence model
