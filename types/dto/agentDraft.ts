export type AgentDirectionType = "inbound" | "outbound";

export interface AgentTypeDto {
  directionType: AgentDirectionType;
  displayName: string;
}

export interface AgentDto {
  name: string;
  voiceProvider: "elevenlabs" | "openai" | "system";
  voiceId: string;
  language: string;
  timezone: string;
}

export interface CallFlowDto {
  greetingPrompt: string;
  systemPrompt: string;
  fallbackPrompt: string;
  transferEnabled: boolean;
  transferNumber?: string;
  postCallSummaryEnabled: boolean;
}

export interface CreateAgentDraftDto {
  type: AgentTypeDto;
  agent: AgentDto;
  callFlow: CallFlowDto;
}

export interface AgentDraftDto extends CreateAgentDraftDto {
  id: string;
  status: "draft" | "ready";
  createdAt: string;
  updatedAt: string;
}
