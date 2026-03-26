import { FieldErrors, UseFormRegister } from "react-hook-form";

import { FormField, FormSection } from "@/components/admin/forms/FormSection";
import { CreateAgentDraftForm } from "@/lib/validation/createAgentDraft";

interface CallFlowSectionProps {
  register: UseFormRegister<CreateAgentDraftForm>;
  errors: FieldErrors<CreateAgentDraftForm>;
  transferEnabled: boolean;
}

export function CallFlowSection({ register, errors, transferEnabled }: CallFlowSectionProps) {
  return (
    <FormSection title="Call Flow" description="Define prompts and call handling behavior.">
      <FormField
        label="Greeting prompt"
        htmlFor="callFlow.greetingPrompt"
        error={errors.callFlow?.greetingPrompt?.message}
      >
        <textarea
          id="callFlow.greetingPrompt"
          rows={3}
          {...register("callFlow.greetingPrompt")}
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
        />
      </FormField>

      <FormField
        label="System prompt"
        htmlFor="callFlow.systemPrompt"
        error={errors.callFlow?.systemPrompt?.message}
      >
        <textarea
          id="callFlow.systemPrompt"
          rows={5}
          {...register("callFlow.systemPrompt")}
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
        />
      </FormField>

      <FormField
        label="Fallback prompt"
        htmlFor="callFlow.fallbackPrompt"
        error={errors.callFlow?.fallbackPrompt?.message}
      >
        <textarea
          id="callFlow.fallbackPrompt"
          rows={3}
          {...register("callFlow.fallbackPrompt")}
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
        />
      </FormField>

      <label className="flex items-center gap-2 text-sm text-slate-700">
        <input type="checkbox" {...register("callFlow.transferEnabled")} />
        Enable transfer to human
      </label>

      {transferEnabled ? (
        <FormField
          label="Transfer number"
          htmlFor="callFlow.transferNumber"
          hint="E.164 format: +14155550123"
          error={errors.callFlow?.transferNumber?.message}
        >
          <input
            id="callFlow.transferNumber"
            {...register("callFlow.transferNumber")}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
          />
        </FormField>
      ) : null}

      <label className="flex items-center gap-2 text-sm text-slate-700">
        <input type="checkbox" {...register("callFlow.postCallSummaryEnabled")} />
        Enable post-call summaries
      </label>
    </FormSection>
  );
}
