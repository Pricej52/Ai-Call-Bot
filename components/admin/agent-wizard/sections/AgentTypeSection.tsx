import { UseFormRegister, FieldErrors } from "react-hook-form";

import { FormField, FormSection } from "@/components/admin/forms/FormSection";
import { CreateAgentDraftForm } from "@/lib/validation/createAgentDraft";

interface AgentTypeSectionProps {
  register: UseFormRegister<CreateAgentDraftForm>;
  errors: FieldErrors<CreateAgentDraftForm>;
}

export function AgentTypeSection({ register, errors }: AgentTypeSectionProps) {
  return (
    <FormSection
      title="Agent Type"
      description="Set up whether this draft handles inbound calls or powers outbound campaigns."
    >
      <FormField label="Type name" htmlFor="type.displayName" error={errors.type?.displayName?.message}>
        <input
          id="type.displayName"
          {...register("type.displayName")}
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
          placeholder="Customer Support Inbound"
        />
      </FormField>

      <FormField label="Direction" htmlFor="type.directionType" error={errors.type?.directionType?.message}>
        <div className="grid gap-3 sm:grid-cols-2">
          <label className="rounded-lg border border-slate-300 p-3 text-sm">
            <input type="radio" value="inbound" {...register("type.directionType")} className="mr-2" />
            Inbound
          </label>
          <label className="rounded-lg border border-slate-300 p-3 text-sm">
            <input type="radio" value="outbound" {...register("type.directionType")} className="mr-2" />
            Outbound
          </label>
        </div>
      </FormField>
    </FormSection>
  );
}
