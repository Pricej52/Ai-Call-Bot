BEGIN;

-- tenant filtering indexes
CREATE INDEX idx_users_tenant_id ON users (tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_clients_tenant_id ON clients (tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_phone_numbers_tenant_id ON phone_numbers (tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_agents_tenant_id ON agents (tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_agent_versions_tenant_id ON agent_versions (tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_talk_tracks_tenant_id ON talk_tracks (tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_cta_rules_tenant_id ON cta_rules (tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_knowledge_sources_tenant_id ON knowledge_sources (tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_webhook_integrations_tenant_id ON webhook_integrations (tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_campaigns_tenant_id ON campaigns (tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_leads_tenant_id ON leads (tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_calls_tenant_id ON calls (tenant_id);
CREATE INDEX idx_call_events_tenant_id ON call_events (tenant_id);
CREATE INDEX idx_transcripts_tenant_id ON transcripts (tenant_id);

-- call lookup and performance indexes
CREATE INDEX idx_calls_provider_call_id ON calls (provider_call_id);
CREATE INDEX idx_calls_started_at ON calls (started_at DESC);
CREATE INDEX idx_calls_status_started_at ON calls (status, started_at DESC);
CREATE INDEX idx_calls_lead_id ON calls (lead_id);
CREATE INDEX idx_calls_campaign_id ON calls (campaign_id);
CREATE INDEX idx_calls_agent_id ON calls (agent_id);
CREATE INDEX idx_calls_phone_number_id ON calls (phone_number_id);
CREATE INDEX idx_calls_from_to ON calls (from_e164, to_e164);
CREATE INDEX idx_call_events_call_id_occurred_at ON call_events (call_id, occurred_at);
CREATE INDEX idx_transcripts_call_id_start ON transcripts (call_id, start_offset_seconds);

COMMIT;
