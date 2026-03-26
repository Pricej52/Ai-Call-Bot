import { AgentDraftDto, CreateAgentDraftDto } from "@/types/dto/agentDraft";

const BASE_URL = "/api/admin/agent-drafts";

async function request<T>(input: RequestInfo | URL, init?: RequestInit): Promise<T> {
  const response = await fetch(input, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Unable to persist agent draft.");
  }

  return (await response.json()) as T;
}

export function createAgentDraft(payload: CreateAgentDraftDto) {
  return request<AgentDraftDto>(BASE_URL, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateAgentDraft(id: string, payload: CreateAgentDraftDto) {
  return request<AgentDraftDto>(`${BASE_URL}/${id}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export function getAgentDraft(id: string) {
  return request<AgentDraftDto>(`${BASE_URL}/${id}`, {
    method: "GET",
  });
}
