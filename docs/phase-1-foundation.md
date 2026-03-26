# Phase 1 — Architecture and Planning

## 1) System Architecture

### High-level components
- **Admin UI (Next.js 15 + TypeScript)**
  - Tenant-scoped administration and wizard-driven agent setup.
  - Prompt/talk-track/CTA editors and operations dashboards.
- **Orchestration API (FastAPI)**
  - Multi-tenant CRUD, auth, wizard state persistence.
  - Inbound/outbound call runtime entrypoints.
  - Prompt composition and tool execution policy.
- **Runtime Workers (Python + Redis queues)**
  - Outbound campaign scheduling, retries, business-hour gating, and webhook delivery retries.
- **PostgreSQL**
  - Source of truth for tenants, agents, prompts, campaigns, calls, transcripts.
- **Redis**
  - Durable queue for call jobs and webhook retries.
  - Ephemeral session state for active call orchestration.
- **Provider adapters**
  - Twilio adapter (telephony abstraction).
  - LLM adapter (OpenAI realtime/voice orchestration).
  - Retrieval adapter (knowledge-base provider abstraction).

### Boundary rules
- `adapters/twilio.py` contains provider-specific webhook/payload parsing only.
- `adapters/llm.py` contains orchestration provider boundary.
- `services/*` only depends on interfaces and domain models.
- API routers are thin transport layers.

## 2) Database Entities and Relationships

### Core multi-tenant hierarchy
- `tenants` 1:N `tenant_users`
- `tenants` 1:N `client_accounts`
- `client_accounts` 1:N `phone_numbers`
- `client_accounts` 1:N `agent_instances`

### Agent and configuration
- `agent_templates` reusable by tenant
- `agent_instances` concrete agent per client/account
- `prompt_versions` versioned layered prompt snapshots per agent
- `talk_tracks` versioned objection/question guidance
- `cta_rules` structured CTA logic blocks
- `knowledge_sources` URL-backed retrieval sources (provider replaceable)
- `webhook_integrations` outbound event sinks
- `agent_wizard_drafts` persisted wizard progress and payload

### Campaign and runtime
- `campaigns` define outbound logic and schedule rules
- `campaign_leads` target contacts
- `call_sessions` inbound/outbound call lifecycle
- `transcript_entries` ordered utterances
- `webhook_deliveries` delivery audit and retries

## 3) API Routes (v1)

### Auth
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`

### Tenancy and client management
- `POST /api/v1/tenants`
- `GET /api/v1/tenants`
- `POST /api/v1/clients`
- `GET /api/v1/clients?tenant_id=...`

### Agent management
- `POST /api/v1/agents`
- `GET /api/v1/agents?tenant_id=...`

### Wizard persistence
- `PUT /api/v1/agent-wizard/draft`

### Runtime webhooks / call session
- `POST /api/v1/calls/webhooks/twilio/inbound`

## 4) UI Route Map (Next.js app router)

- `/login`
- `/tenants`
- `/tenants/[tenantId]/clients`
- `/tenants/[tenantId]/phone-numbers`
- `/tenants/[tenantId]/agents`
- `/tenants/[tenantId]/agents/new/step-1-agent-type`
- `/tenants/[tenantId]/agents/new/step-2-agent`
- `/tenants/[tenantId]/agents/new/step-3-call-flow`
- `/tenants/[tenantId]/agents/new/step-4-overview`
- `/tenants/[tenantId]/prompts`
- `/tenants/[tenantId]/talk-tracks`
- `/tenants/[tenantId]/cta-rules`
- `/tenants/[tenantId]/campaigns`
- `/tenants/[tenantId]/calls`
- `/tenants/[tenantId]/calls/[callSessionId]/transcript`
- `/tenants/[tenantId]/webhook-deliveries`

## 5) Phased Implementation Checklist

### Phase 1 (current)
- [x] Architecture and design artifacts
- [x] Initial relational model in backend domain
- [x] API contract baseline for first workflows

### Phase 2
- [x] FastAPI service skeleton with typed DTOs
- [x] Auth endpoints
- [x] Tenant/client/agent CRUD foundations
- [x] Wizard state persistence endpoint
- [x] Twilio inbound webhook resolver foundation
- [x] Call session model and persistence
- [ ] Add RBAC dependency middleware
- [ ] Add alembic migration pipeline and CI migration checks

### Phase 3
- [ ] Next.js admin app scaffolding
- [ ] Agent create wizard UI for steps 1–4
- [ ] Agent list page
- [ ] Transcript viewer page

### Phase 4
- [ ] Inbound call conversation orchestrator (LLM adapter + tools)
- [ ] Outbound campaign queue + worker
- [ ] Voicemail handling + disposition rules
- [ ] Webhook posting service + retry worker
- [ ] End-to-end smoke tests across inbound/outbound flows
