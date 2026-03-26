import { FieldErrors, UseFormRegister } from "react-hook-form";

import { FormField, FormSection } from "@/components/admin/forms/FormSection";
import { CreateAgentDraftForm } from "@/lib/validation/createAgentDraft";

interface AgentSectionProps {
  register: UseFormRegister<CreateAgentDraftForm>;
  errors: FieldErrors<CreateAgentDraftForm>;
}

export function AgentSection({ register, errors }: AgentSectionProps) {
  return (
    <FormSection title="Agent" description="Configure identity, voice, and locale details.">
      <div className="grid gap-4 md:grid-cols-2">
        <FormField label="Agent name" htmlFor="agent.name" error={errors.agent?.name?.message}>
          <input
            id="agent.name"
            {...register("agent.name")}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
            placeholder="Ava"
          />
        </FormField>

        <FormField label="Voice provider" htmlFor="agent.voiceProvider" error={errors.agent?.voiceProvider?.message}>
          <select
            id="agent.voiceProvider"
            {...register("agent.voiceProvider")}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
          >
            <option value="elevenlabs">ElevenLabs</option>
            <option value="openai">OpenAI</option>
            <option value="system">System</option>
          </select>
        </FormField>

        <FormField label="Voice ID" htmlFor="agent.voiceId" error={errors.agent?.voiceId?.message}>
          <input
            id="agent.voiceId"
            {...register("agent.voiceId")}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
            placeholder="voice_en_us_01"
          />
        </FormField>

        <FormField label="Language" htmlFor="agent.language" error={errors.agent?.language?.message}>
          <input
            id="agent.language"
            {...register("agent.language")}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
            placeholder="en-US"
          />
        </FormField>

        <FormField label="Timezone" htmlFor="agent.timezone" error={errors.agent?.timezone?.message}>
          <input
            id="agent.timezone"
            {...register("agent.timezone")}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
            placeholder="America/New_York"
          />
        </FormField>
      </div>
    </FormSection>
  );
}
