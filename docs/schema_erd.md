# White-Label AI Voice Agent Platform — ERD

```mermaid
erDiagram
    tenants ||--o{ users : has
    tenants ||--o{ clients : has
    tenants ||--o{ phone_numbers : has
    tenants ||--o{ agents : has
    agents ||--o{ agent_versions : versions
    agent_versions ||--o{ talk_tracks : includes
    agent_versions ||--o{ cta_rules : includes
    tenants ||--o{ knowledge_sources : has
    agent_versions }o--o{ knowledge_sources : references
    tenants ||--o{ webhook_integrations : has
    clients ||--o{ campaigns : has
    tenants ||--o{ campaigns : has
    campaigns ||--o{ leads : contains
    clients ||--o{ leads : has
    tenants ||--o{ leads : has
    phone_numbers ||--o{ calls : receives_or_places
    agents ||--o{ calls : handles
    agent_versions ||--o{ calls : executes
    campaigns ||--o{ calls : drives
    leads ||--o{ calls : concerns
    clients ||--o{ calls : belongs_to
    tenants ||--o{ calls : owns
    calls ||--o{ call_events : emits
    calls ||--o{ transcripts : has

    tenants {
      uuid id PK
      text name
      text slug UK
      text status
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    users {
      uuid id PK
      uuid tenant_id FK
      text email
      text full_name
      text role
      text status
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    clients {
      uuid id PK
      uuid tenant_id FK
      text name
      text external_ref
      jsonb metadata
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    phone_numbers {
      uuid id PK
      uuid tenant_id FK
      uuid client_id FK
      text e164 UK_per_tenant
      text provider
      text direction
      text status
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    agents {
      uuid id PK
      uuid tenant_id FK
      uuid client_id FK
      text name
      text direction_mode
      text status
      uuid current_version_id FK
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    agent_versions {
      uuid id PK
      uuid tenant_id FK
      uuid agent_id FK
      int version_number
      text prompt_text
      jsonb model_config
      boolean is_published
      uuid created_by_user_id FK
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    talk_tracks {
      uuid id PK
      uuid tenant_id FK
      uuid agent_version_id FK
      text track_type
      int sort_order
      text content
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    cta_rules {
      uuid id PK
      uuid tenant_id FK
      uuid agent_version_id FK
      text name
      int priority
      jsonb trigger_config
      jsonb action_config
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    knowledge_sources {
      uuid id PK
      uuid tenant_id FK
      uuid client_id FK
      text source_type
      text uri
      text status
      jsonb metadata
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    webhook_integrations {
      uuid id PK
      uuid tenant_id FK
      uuid client_id FK
      text name
      text target_url
      text event_type
      text auth_type
      jsonb auth_config
      boolean is_active
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    campaigns {
      uuid id PK
      uuid tenant_id FK
      uuid client_id FK
      uuid agent_id FK
      text name
      text channel
      text status
      timestamptz starts_at
      timestamptz ends_at
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    leads {
      uuid id PK
      uuid tenant_id FK
      uuid client_id FK
      uuid campaign_id FK
      text first_name
      text last_name
      text phone_e164
      text email
      text status
      jsonb attributes
      timestamptz created_at
      timestamptz updated_at
      timestamptz deleted_at
    }

    calls {
      uuid id PK
      uuid tenant_id FK
      uuid client_id FK
      uuid campaign_id FK
      uuid lead_id FK
      uuid agent_id FK
      uuid agent_version_id FK
      uuid phone_number_id FK
      text direction
      text provider_call_id
      text from_e164
      text to_e164
      text status
      int duration_seconds
      timestamptz started_at
      timestamptz ended_at
      timestamptz created_at
      timestamptz updated_at
    }

    call_events {
      uuid id PK
      uuid tenant_id FK
      uuid call_id FK
      text event_type
      int seq_no
      jsonb payload
      timestamptz occurred_at
      timestamptz created_at
      timestamptz updated_at
    }

    transcripts {
      uuid id PK
      uuid tenant_id FK
      uuid call_id FK
      text speaker
      text content
      numeric start_offset_seconds
      numeric end_offset_seconds
      numeric confidence
      timestamptz created_at
      timestamptz updated_at
    }
```
