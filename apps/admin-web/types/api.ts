export type AgentType = "inbound" | "outbound";

export interface Agent {
  id: string;
  tenant_id: string;
  client_account_id: string;
  type: AgentType;
  name: string;
  language: string;
  voice: string;
  call_flow: Record<string, unknown>;
  is_published: boolean;
}

export interface CreateAgentPayload {
  tenant_id: string;
  client_account_id: string;
  type: AgentType;
  name: string;
  phone_number_id?: string;
  template_id?: string;
  language: string;
  voice: string;
  voice_settings?: Record<string, unknown>;
  call_flow?: Record<string, unknown>;
  meeting_settings?: Record<string, unknown>;
}

export interface Campaign {
  id: string;
  name: string;
  leadsCount?: number;
}

export interface CreateCampaignPayload {
  name: string;
  leads: string;
}

export interface CallLog {
  id: string;
  provider_call_sid: string;
  from_number: string;
  to_number: string;
  direction: string;
  status: string;
  summary?: string | null;
  started_at: string;
}

export interface TenantSettingsPayload {
  tenantName: string;
  timezone: string;
  supportEmail: string;
}
