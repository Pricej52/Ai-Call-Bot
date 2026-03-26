import { FormSection } from "@/components/admin/forms/FormSection";
import { CreateAgentDraftForm } from "@/lib/validation/createAgentDraft";

interface OverviewSectionProps {
  values: CreateAgentDraftForm;
  draftId?: string;
}

export function OverviewSection({ values, draftId }: OverviewSectionProps) {
  return (
    <FormSection title="Overview" description="Review your configuration before final save.">
      <div className="grid gap-4 text-sm text-slate-700 md:grid-cols-2">
        <div>
          <h3 className="font-semibold text-slate-900">Agent Type</h3>
          <p>Name: {values.type.displayName}</p>
          <p>Direction: {values.type.directionType}</p>
        </div>
        <div>
          <h3 className="font-semibold text-slate-900">Agent</h3>
          <p>Name: {values.agent.name}</p>
          <p>Voice: {values.agent.voiceProvider} / {values.agent.voiceId}</p>
          <p>Locale: {values.agent.language} ({values.agent.timezone})</p>
        </div>
        <div className="md:col-span-2">
          <h3 className="font-semibold text-slate-900">Call Flow</h3>
          <p>Greeting: {values.callFlow.greetingPrompt}</p>
          <p>Transfer enabled: {values.callFlow.transferEnabled ? "Yes" : "No"}</p>
          {values.callFlow.transferEnabled ? <p>Transfer number: {values.callFlow.transferNumber}</p> : null}
          <p>Post-call summary: {values.callFlow.postCallSummaryEnabled ? "Yes" : "No"}</p>
        </div>
      </div>
      {draftId ? <p className="text-xs text-slate-400">Draft ID: {draftId}</p> : null}
      <p className="rounded-md bg-slate-50 p-3 text-xs text-slate-500">
        Twilio execution is intentionally disabled in this flow. Only backend draft persistence is used.
      </p>
    </FormSection>
  );
}
