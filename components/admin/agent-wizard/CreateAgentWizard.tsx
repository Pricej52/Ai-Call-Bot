"use client";

import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import { createAgentDraft, getAgentDraft, updateAgentDraft } from "@/lib/api/agentDrafts";
import { createAgentDraftSchema, CreateAgentDraftForm } from "@/lib/validation/createAgentDraft";
import { AgentTypeSection } from "@/components/admin/agent-wizard/sections/AgentTypeSection";
import { AgentSection } from "@/components/admin/agent-wizard/sections/AgentSection";
import { CallFlowSection } from "@/components/admin/agent-wizard/sections/CallFlowSection";
import { OverviewSection } from "@/components/admin/agent-wizard/sections/OverviewSection";
import { Stepper } from "@/components/admin/agent-wizard/Stepper";

const STEPS = ["Agent Type", "Agent", "Call Flow", "Overview"];

const STEP_FIELDS: Array<Array<keyof CreateAgentDraftForm>> = [["type"], ["agent"], ["callFlow"], []];

const defaultValues: CreateAgentDraftForm = {
  type: {
    directionType: "inbound",
    displayName: "",
  },
  agent: {
    name: "",
    voiceProvider: "system",
    voiceId: "",
    language: "en-US",
    timezone: "America/New_York",
  },
  callFlow: {
    greetingPrompt: "",
    systemPrompt: "",
    fallbackPrompt: "",
    transferEnabled: false,
    transferNumber: "",
    postCallSummaryEnabled: true,
  },
};

export function CreateAgentWizard() {
  const [step, setStep] = useState(0);
  const [draftId, setDraftId] = useState<string | undefined>();
  const [saveState, setSaveState] = useState<"idle" | "saving" | "saved" | "error">("idle");
  const searchParams = useSearchParams();

  const form = useForm<CreateAgentDraftForm>({
    resolver: zodResolver(createAgentDraftSchema),
    mode: "onBlur",
    defaultValues,
  });

  const transferEnabled = form.watch("callFlow.transferEnabled");
  const formValues = form.watch();

  useEffect(() => {
    const existingDraftId = searchParams.get("draftId");

    if (!existingDraftId) {
      return;
    }

    const loadDraft = async () => {
      try {
        const draft = await getAgentDraft(existingDraftId);
        form.reset(draft);
        setDraftId(draft.id);
      } catch {
        setSaveState("error");
      }
    };

    void loadDraft();
  }, [form, searchParams]);

  useEffect(() => {
    const timeout = setTimeout(() => {
      const values = form.getValues();

      if (!values.type.displayName && !values.agent.name && !values.callFlow.greetingPrompt) {
        return;
      }

      const saveDraft = async () => {
        try {
          setSaveState("saving");
          if (draftId) {
            await updateAgentDraft(draftId, values);
          } else {
            const draft = await createAgentDraft(values);
            setDraftId(draft.id);
          }
          setSaveState("saved");
        } catch {
          setSaveState("error");
        }
      };

      void saveDraft();
    }, 700);

    return () => clearTimeout(timeout);
  }, [formValues, draftId, form]);

  const canGoNext = step < STEPS.length - 1;
  const canGoBack = step > 0;

  const stepBody = useMemo(() => {
    switch (step) {
      case 0:
        return <AgentTypeSection register={form.register} errors={form.formState.errors} />;
      case 1:
        return <AgentSection register={form.register} errors={form.formState.errors} />;
      case 2:
        return (
          <CallFlowSection
            register={form.register}
            errors={form.formState.errors}
            transferEnabled={transferEnabled}
          />
        );
      case 3:
        return <OverviewSection values={form.getValues()} draftId={draftId} />;
      default:
        return null;
    }
  }, [draftId, form, step, transferEnabled]);

  const handleNext = async () => {
    const fields = STEP_FIELDS[step];
    const valid = await form.trigger(fields as any, { shouldFocus: true });

    if (!valid) {
      return;
    }

    if (canGoNext) {
      setStep((previous) => previous + 1);
    }
  };

  const handleSave = async () => {
    const valid = await form.trigger(undefined, { shouldFocus: true });
    if (!valid) {
      return;
    }

    try {
      setSaveState("saving");
      const values = form.getValues();
      if (draftId) {
        await updateAgentDraft(draftId, values);
      } else {
        const draft = await createAgentDraft(values);
        setDraftId(draft.id);
      }
      setSaveState("saved");
    } catch {
      setSaveState("error");
    }
  };

  return (
    <main className="mx-auto max-w-5xl space-y-6 px-6 py-8">
      <header>
        <h1 className="text-2xl font-semibold text-slate-900">Create Agent</h1>
        <p className="text-sm text-slate-500">Draft setup is auto-saved to backend state only.</p>
      </header>

      <Stepper steps={STEPS} activeStep={step} />

      {stepBody}

      <footer className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-4">
        <div className="text-xs text-slate-500">
          {saveState === "saving" ? "Saving draft..." : null}
          {saveState === "saved" ? "Draft saved" : null}
          {saveState === "error" ? "Unable to save draft" : null}
        </div>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => canGoBack && setStep((previous) => previous - 1)}
            disabled={!canGoBack}
            className="rounded-lg border border-slate-300 px-4 py-2 text-sm text-slate-700 disabled:opacity-50"
          >
            Back
          </button>
          {canGoNext ? (
            <button
              type="button"
              onClick={handleNext}
              className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
            >
              Next
            </button>
          ) : (
            <button
              type="button"
              onClick={handleSave}
              className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
            >
              Save Draft
            </button>
          )}
        </div>
      </footer>
    </main>
  );
}
