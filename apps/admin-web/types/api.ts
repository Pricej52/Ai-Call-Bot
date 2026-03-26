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
  meeting_settings?: Record<string, unknown>;
  phone_number_id?: string | null;
  twilio_phone_number?: string | null;
  base_prompt?: string | null;
  talk_tracks?: string | null;
  cta_instructions?: string | null;
  voicemail_behavior?: string | null;
  webhook_url?: string | null;
  business_hours?: Record<string, unknown>;
  status?: "draft" | "published";
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
  twilio_phone_number?: string;
  base_prompt?: string;
  talk_tracks?: string;
  cta_instructions?: string;
  voicemail_behavior?: string;
  webhook_url?: string;
  business_hours?: Record<string, unknown>;
  status?: "draft" | "published";
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
  ended_at?: string | null;
  disposition?: string | null;
}

export interface TranscriptEntry {
  id: string;
  speaker: string;
  content: string;
  sequence: number;
  created_at: string;
}

export interface CallLogDetail extends CallLog {
  transcript_entries: TranscriptEntry[];
}

export interface DashboardStats {
  total_agents: number;
  total_calls: number;
  total_campaigns: number;
}

export interface TenantSettingsPayload {
  tenantName: string;
  timezone: string;
  supportEmail: string;
}
