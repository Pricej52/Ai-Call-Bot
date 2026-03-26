# Design Choices

## 1) Multi-tenant isolation
- Every business-domain table includes a required `tenant_id` with an explicit FK to `tenants(id)`.
- Tenant-scoped uniqueness constraints are used where collisions are likely (`users.email`, `phone_numbers.e164`, `knowledge_sources.uri`, `calls.provider_call_id`).
- A dedicated tenant index is added on all major tables for efficient tenant filtering.

## 2) Versioning for prompts/config
- `agents` is the stable identity.
- `agent_versions` stores immutable-ish prompt and runtime snapshots (`prompt_text`, `model_config`, `voice_config`, `runtime_config`).
- `agents.current_version_id` points to the currently active version for low-latency routing.
- `talk_tracks` and `cta_rules` belong to `agent_versions`, ensuring behavior snapshots are reproducible.

## 3) Inbound and outbound support
- `agents.direction_mode` uses enum: `INBOUND`, `OUTBOUND`, `BOTH`.
- `phone_numbers.direction` also supports routing constraints.
- `calls.direction` captures per-call runtime mode (`INBOUND` or `OUTBOUND`).

## 4) Soft delete strategy
- Soft delete (`deleted_at`) is applied to mutable/configuration entities: tenants, users, clients, phone numbers, agents, versions, talk tracks, cta rules, knowledge sources, webhooks, campaigns, leads.
- Operational event data (`calls`, `call_events`, `transcripts`) stays physically retained for audit/analytics integrity.

## 5) Explicit relational integrity
- All relationships are modeled via explicit foreign keys.
- M:N relationship between `agent_versions` and `knowledge_sources` is modeled through `agent_version_knowledge_sources`.

## 6) Timestamp standardization
- Every table has `created_at` and `updated_at`.
- Domain time fields are included where appropriate (`started_at`, `ended_at`, `occurred_at`, offsets in transcripts).

## 7) Indexing strategy
- Tenant-filter indexes are partial (`WHERE deleted_at IS NULL`) for soft-deleted tables.
- Call lookup indexes target common access patterns:
  - Provider callback lookups (`provider_call_id`)
  - Recent call feeds (`started_at DESC`, `status + started_at`)
  - Joins (`lead_id`, `campaign_id`, `agent_id`, `phone_number_id`)
  - Event and transcript timelines (`call_id + occurred_at`, `call_id + start_offset_seconds`)
