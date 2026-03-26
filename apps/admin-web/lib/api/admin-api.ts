import { apiClient } from "@/lib/api/client";
import {
  Agent,
  CallLog,
  Campaign,
  CreateAgentPayload,
  CreateCampaignPayload,
  TenantSettingsPayload,
} from "@/types/api";

export async function listAgents(tenantId: string) {
  const { data } = await apiClient.get<Agent[]>(`/agents?tenant_id=${tenantId}`);
  return data;
}

export async function createAgent(payload: CreateAgentPayload) {
  const { data } = await apiClient.post<Agent>("/agents", payload);
  return data;
}

export async function updateAgent(agentId: string, payload: Partial<CreateAgentPayload>) {
  const { data } = await apiClient.patch<Agent>(`/agents/${agentId}`, payload);
  return data;
}

export async function deleteAgent(agentId: string) {
  await apiClient.delete(`/agents/${agentId}`);
}

export async function createCampaign(payload: CreateCampaignPayload) {
  const { data } = await apiClient.post<Campaign>("/campaigns", payload);
  return data;
}

export async function listCalls() {
  const { data } = await apiClient.get<CallLog[]>("/calls");
  return data;
}

export async function saveTenantSettings(payload: TenantSettingsPayload) {
  return payload;
}
